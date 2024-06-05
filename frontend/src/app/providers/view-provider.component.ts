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

}

