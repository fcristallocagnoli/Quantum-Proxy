import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Account } from '@app/_models';
import { System } from '@app/_models/system';
import { AccountService, AlertService, ProviderService } from '@app/_services';
import { SystemService } from '@app/_services/system.service';
import { first } from 'rxjs';

@Component({
  selector: 'app-systems',
  templateUrl: './systems.component.html',
})
export class SystemsComponent {
  systems?: System[];
  showScroll: boolean = false;
  isFetchingData: boolean = false;
  fetchingFrom: string = "";
  account?: Account | null;

  constructor(
    private systemService: SystemService,
    private providerService: ProviderService,
    private accountService: AccountService,
    private alertService: AlertService,
    private route: ActivatedRoute,
  ) {
    this.accountService.account.subscribe(x => this.account = x);
  }

  ngOnInit() {
    const pid = this.route.snapshot.params['pid'];
    if (pid) {
      this.providerService.getByPid(pid)
        .pipe(first())
        .subscribe(provider => {
          let providerSystems = provider["backends_ids"] ?? [];
          this.systemService.getAll()
            .pipe(first())
            .subscribe(systems => {
              this.systems = systems.filter(s => providerSystems.includes(s.id));
            });
        });
    } else {
      this.systemService.getAll()
        .pipe(first())
        .subscribe(systems => {
          this.systems = systems.sort((a, b) =>
            this.compareSystems(a, b));
        });
    }
  }

  compareSystems(a: System, b: System) {
    // Desplazamos los de estado desconocido al final
    if (a.status === undefined || b.status === undefined) {
      return 1;
    }
    let dateA = new Date(a.last_checked);
    let dateB = new Date(b.last_checked);
    let comparison = dateB.getTime() - dateA.getTime();
    return comparison;
  }

  updateSystem(system: System) {
    this.isFetchingData = true;
    this.fetchingFrom = system.provider.provider_from ?? system.provider.provider_id;
    this.systemService.refreshData({ "_id": system.provider.provider_id })
      .subscribe({
        next: () => {
          this.isFetchingData = false;
          for (let i = 3; i > 0; i--) {
            setTimeout(() => {
              this.alertService.clear();
              this.alertService.success(`
                <h4>System updated successfully</h4>
                <p>Page will reload in ${i}seg</p>
              `);
            }, (3 - i) * 1000);
          }
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        },
        error: error => {
          this.alertService.error(`
            <h4>Error updating system</h4>
            <p>${error}</p>
          `);
        }
      });
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
