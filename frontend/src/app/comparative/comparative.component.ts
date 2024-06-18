import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Provider, System } from '@app/_models';
import { ProviderService, SystemService } from '@app/_services';

@Component({
    selector: 'app-comparative',
    templateUrl: './comparative.component.html',
})
export class ComparativeComponent {
    entity1: string
    entity2: string

    providers: Provider[] = []
    systems: System[] = []

    // Inicializa los valores por defecto
    selectedProvider1: string = 'native.ionq';
    selectedProvider2: string = 'native.ibm_quantum';

    selectedSystem1: string = 'forte-1';
    selectedSystem2: string = 'forte-1-aws';

    constructor(
        private router: Router,
        private providerService: ProviderService,
        private systemService: SystemService
    ) { }

    ngOnInit(): void {
        this.providerService.getAll().subscribe(providers => {
            this.providers = this.transformFromPython(providers);
            this.providers.sort((a, b) => a.name!.localeCompare(b.name!));
        });
        this.systemService.getAll().subscribe(systems => {
            this.systems = systems;
            this.systems.sort((a, b) => a.backend_name!.localeCompare(b.backend_name!));
            this.systems.forEach(system => {
                console.log(this.normalizeName(system.backend_name!));
            });
        });
    }

    getFilteredProviders(selectedProvider: string): Provider[] {
        return this.providers.filter(provider => provider.pid !== selectedProvider);
    }

    getFilteredSystems(selectedSystem: string): System[] {
        return this.systems.filter(system => this.normalizeNameToURL(system) !== selectedSystem);
    }

    compare(entity1: any, entity2: any) {
        this.router.navigateByUrl(`/compare/${entity1}-vs-${entity2}`);
    }

    transformFromPython(providers: any[]): Provider[] {
        return providers.map(provider => {
            return {
                ...provider,
                fromThirdParty: provider.from_third_party,
                fetchMethod: (provider.backend_request) ? provider.backend_request.fetch_method : null,
                thirdParty: (provider.third_party) ? {
                    id: provider.third_party.third_party_id,
                    name: provider.third_party.third_party_name
                } : null,
                systems: provider.backends_ids
            };
        });
    }

    normalizeName(name: string): string {
        return name.replace(/ /g, '-').replace(/\b\w/g, l => l.toUpperCase())
    }

    normalizeNameToURL(system: System): string {
        let bname = system.backend_name;
        let providerFrom = system.provider.provider_from;

        bname = bname.toLowerCase().replace(/ /g, '-');
        if (providerFrom) {
            bname = `${bname}-${providerFrom.toLowerCase()}`;
        }
        return bname;
    }
}
