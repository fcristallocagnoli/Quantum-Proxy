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

  getDescription(provider: Provider, scope: string = 'all') {
    let description = provider.description
    if (provider.description instanceof Object) {
      switch (scope) {
        case 'short':
          description = provider.description.short_description
          break
        case 'long':
          description = provider.description.long_description
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

  transformFromPython(providers: any[]): Provider[] {
    return providers.map(provider => {
      return {
        ...provider,
        fetchMethod: (provider.backend_request) ? provider.backend_request.fetch_method : null,
      };
    });
  }
}

