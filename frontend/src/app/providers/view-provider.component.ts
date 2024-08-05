import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Provider, System } from '@app/_models';
import { SystemService } from '@app/_services';
import { ProviderService } from '@app/_services/provider.service';
import { first } from 'rxjs';

@Component({
  templateUrl: 'view-provider.component.html',
})
export class ViewProviderComponent implements OnInit {
  provider?: Provider
  systems?: System[]

  constructor(
    private route: ActivatedRoute,
    private providerService: ProviderService,
    private systemService: SystemService
  ) { }

  ngOnInit(): void {
    const pid = this.route.snapshot.params['pid']
    this.providerService.getByPid(pid)
      .pipe(first())
      .subscribe(provider => {
        this.provider = provider;
        let providerSystems = provider["backends_ids"] ?? [];
        this.systemService.getAll()
          .pipe(first())
          .subscribe(systems => {
            this.systems = systems.filter(s => providerSystems.includes(s.id));
            this.systems = this.sortSystems(this.systems);
          });
      });
  }

  // sort systems by status, those that are running, online or available first
  sortSystems(systems: System[]) {
    return systems.sort((a, b) => {
      let statusA = a.status ?? "N/A"
      let statusB = b.status ?? "N/A"
      if (["running", "online", "available"].includes(statusA) &&
        !["running", "online", "available"].includes(statusB)) {
        return -1
      }
      if (!["running", "online", "available"].includes(statusA) &&
        ["running", "online", "available"].includes(statusB)) {
        return 1
      }
      return 0
    })
  }

  getDescription(provider: Provider, scope: string = 'all') {
    let description = provider.description
    if (provider.description instanceof Object) {
      switch (scope) {
        case 'summary':
          description = provider.description.short_description
          break
        case 'history':
          description = provider.description.history
          break
        case 'all':
          description = `
            <h2>Summary</h2>
            <p>${provider.description.short_description}</p>
            <h2>Description</h2>
            <p>${provider.description.long_description}</p>
            <h2>History</h2>
            <p>${provider.description.history}</p>
            `
          break
      }
    }
    return description
  }

  countSystemsOnline() {
    return this.systems?.filter(
      s => ["running", "online", "available"]
        .includes(s.status ?? "N/A")).length
  }

  // Convierte tiempo en milisegundos a tiempo de espera con el formato de IonQ
  convertFromMs(millisecStr: string | undefined): string {
    if (millisecStr === undefined) {
      return "N/A";
    }
    let millisec = parseInt(millisecStr);

    // Convertir milisegundos a segundos
    let seconds = Math.floor(millisec / 1000);

    // Calcular días, horas y minutos
    const mins = Math.floor(seconds / 60);
    seconds = seconds % 60;
    const hours = Math.floor(mins / 60);
    const minutes = mins % 60;
    const days = Math.floor(hours / 24);
    const remainingHours = hours % 24;

    let avgTimeInQueue = "";

    if (days > 30) {
      avgTimeInQueue = "> 1month";
    } else if (days > 1) {
      avgTimeInQueue = `${days}d ${remainingHours}hrs ${minutes}min`;
    } else if (remainingHours > 1) {
      avgTimeInQueue = `${remainingHours}hrs ${minutes}min`;
    } else if (minutes > 1) {
      avgTimeInQueue = `${minutes}min`;
    } else {
      avgTimeInQueue = "< 1min";
    }

    return avgTimeInQueue;
  }

}

