import { Component, OnInit } from '@angular/core';
import { Provider } from '@app/_models';
import { ProviderService } from '@app/_services/provider.service';
import { first } from 'rxjs';

@Component({
  templateUrl: 'providers.component.html',
})
export class ProvidersComponent implements OnInit {
  providers?: Provider[];

  constructor(private providerService: ProviderService) { }

  ngOnInit() {
    this.providerService.getAll()
      .pipe(first())
      .subscribe(providers => {
        this.providers = this.transformFromPython(providers);
      });
  }

  // TODO: Simplificarlo al igual que en 'systems' ¿?
  // ¿se podría usar los mismos nombres que en python?
  // ¿o merece la pena cambiarlos?
  // recorre el array de providers, y cambia el nombre de la propiedad from_third_party a fromThirdParty
  // y los atrubutos de third_party (third_party_name y third_party_id) a id y name
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
        systems: provider.backends_ids,
        lastChecked: provider.last_checked
      };
    });
  }
}

