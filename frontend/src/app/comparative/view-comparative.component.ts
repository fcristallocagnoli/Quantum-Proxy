import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
    templateUrl: 'view-comparative.component.html',
})
export class ViewComparativeComponent implements OnInit {
    entity1: string
    entity2: string

    constructor(
        private route: ActivatedRoute,
        private router: Router,
    ) { }

    ngOnInit(): void {
        let versus: string = this.route.snapshot.params['versus']
        let result = versus.match(/(?<ent1>(\w|.)+)-vs-(?<ent2>(\w|.)+)/);

        if (!result) {
            this.router.navigateByUrl('/');
        }

        this.entity1 = result?.groups!["ent1"] ?? '';
        this.entity2 = result?.groups!["ent2"] ?? '';
    }

}

