import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NgbdModalContent } from '@app/_components/properties.component';
import { System } from '@app/_models';
import { SystemService } from '@app/_services';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { first } from 'rxjs';

@Component({
    templateUrl: 'view-system.component.html',
})
export class ViewSystemComponent implements OnInit {
    bid: string
    system?: System

    constructor(private route: ActivatedRoute, private systemService: SystemService, private modalService: NgbModal) { }

    ngOnInit(): void {
        this.bid = this.route.snapshot.params['bid']
        this.systemService.getByBid(this.bid)
            .pipe(first())
            .subscribe(system => this.system = system);
    }

    openModal() {
        const modalRef = this.modalService.open(NgbdModalContent);
        modalRef.componentInstance.characterization = this.system?.characterization;
    }

}
