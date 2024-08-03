import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Provider, System } from '@app/_models';
import { ProviderService, SystemService } from '@app/_services';

@Component({
    templateUrl: 'compare-providers.component.html',
})
export class CompareProvidersComponent implements OnInit {
    entity1: string
    entity2: string

    provider1: Provider
    provider2: Provider

    systemsP1: System[]
    systemsP2: System[]

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private providerService: ProviderService,
        private systemService: SystemService
    ) { }

    ngOnInit(): void {
        let versus: string = this.route.snapshot.params['versus']
        let result = versus.match(/(?<ent1>(\w|.)+)-vs-(?<ent2>(\w|.)+)/);

        if (!result) {
            this.router.navigateByUrl('/');
        }

        this.entity1 = result?.groups!["ent1"] ?? '';
        this.entity2 = result?.groups!["ent2"] ?? '';

        this.providerService.getByPid(this.entity1).subscribe(provider => {
            this.provider1 = provider;
            this.systemService.getAll().subscribe(systems => {
                this.systemsP1 = systems.filter(s => provider.backends_ids.includes(s.id));
                this.systemsP1 = this.sortSystems(this.systemsP1);
            });
        });
        this.providerService.getByPid(this.entity2).subscribe(provider => {
            this.provider2 = provider;
            this.systemService.getAll().subscribe(systems => {
                this.systemsP2 = systems.filter(s => provider.backends_ids.includes(s.id));
                this.systemsP2 = this.sortSystems(this.systemsP2);
            });
        });
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
                    <h2>History</h2>
                    <p>${provider.description.history}</p>
                    `
                    break
            }
        }
        return description
    }

    getUnionAttributes() {
        const keys1 = Object.keys(this.provider1);
        const keys2 = Object.keys(this.provider2);
        const unionKeys = keys1.concat(keys2.filter(key => !keys1.includes(key)));
        return unionKeys;
    }

    private sortSystems(systems: System[]) {
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

    countSystemsOnline(systems: System[]) {
        return systems?.filter(
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

