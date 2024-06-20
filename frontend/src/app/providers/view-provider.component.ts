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
    pid: string
    provider?: Provider
    systems?: System[]

    constructor(
        private route: ActivatedRoute,
        private providerService: ProviderService,
        private systemService: SystemService
    ) { }

    ngOnInit(): void {
        this.pid = this.route.snapshot.params['pid']
        this.providerService.getByPid(this.pid)
            .pipe(first())
            .subscribe(provider => this.provider = provider);
        this.systemService.getAll()
            .pipe(first())
            .subscribe(systems => {
                this.systems = systems.filter(s => s.provider.provider_id === this.provider?.id)
            });
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

