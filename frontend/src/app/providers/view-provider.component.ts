import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Provider } from '@app/_models';
import { ProviderService } from '@app/_services/provider.service';
import { first } from 'rxjs';

@Component({
    templateUrl: 'view-provider.component.html',
})
export class ViewProviderComponent implements OnInit {
    pid: string
    provider?: Provider

    constructor(private route: ActivatedRoute, private providerService: ProviderService) { }

    ngOnInit(): void {
        this.pid = this.route.snapshot.params['pid']
        this.providerService.getByPid(this.pid)
            .pipe(first())
            .subscribe(provider => this.provider = provider);
    }

    getDescription(provider: Provider, scope: string = 'all') {
        let description: string = ''
        if (provider.description instanceof Object) {
            switch (scope) {
                case 'summary':
                    description = provider.description.summary
                    break
                case 'history':
                    description = provider.description.history
                    break
                case 'all':
                    description = `
                    <h2>Summary</h2>
                    ${provider.description.summary}
                    <h2>History</h2>
                    ${provider.description.history}
                    `
                    break
            }
        }
        return description
    }

}

