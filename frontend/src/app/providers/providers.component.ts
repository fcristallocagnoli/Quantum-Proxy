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
        console.log(providers);
      });
  }

  // recorre el array de providers, y cambia el nombre de la propiedad from_third_party a fromThirdParty
  // y los atrubutos de third_party (third_party_name y third_party_id) a id y name
  transformFromPython(providers: any[]): Provider[] {
    return providers.map(provider => {
      return {
        ...provider,
        fromThirdParty: provider.from_third_party,
        thirdParty: (provider.third_party) ? {
          id: provider.third_party.third_party_id,
          name: provider.third_party.third_party_name
        } : null,
      };
    });
  }
}

