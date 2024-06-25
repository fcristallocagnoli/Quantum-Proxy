import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { System } from '@app/_models';
import { SystemService } from '@app/_services';

@Component({
    templateUrl: 'compare-systems.component.html',
})
export class CompareSystemsComponent implements OnInit {
    entity1: string
    entity2: string

    system1: System
    system2: System

    constructor(
        private route: ActivatedRoute,
        private router: Router,
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

        this.systemService.getByBid(this.entity1).subscribe(system => {
            this.system1 = system;
        });
        this.systemService.getByBid(this.entity2).subscribe(system => {
            this.system2 = system;
        });
    }

    normalizeName(name: string): string {
        return name.replace(/ /g, '-').replace(/\b\w/g, l => l.toUpperCase())
    }

}

