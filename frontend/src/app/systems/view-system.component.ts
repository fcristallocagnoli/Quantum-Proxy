import { JsonPipe } from '@angular/common';
import { Component, Input, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { System } from '@app/_models';
import { SystemService } from '@app/_services';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
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


@Component({
    selector: 'ngbd-modal-content',
    standalone: true,
    template: `
    <div class="modal-header">
        <h4 class="modal-title">Characterization</h4>
        <button type="button" class="btn-close" aria-label="Close" (click)="activeModal.dismiss('Cross click')"></button>
    </div>
    <div class="modal-body">
        <pre>{{ characterization | json }}</pre>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-outline-dark" (click)="activeModal.close('Close click')">Close</button>
    </div>
    `,
    imports: [JsonPipe]
})
export class NgbdModalContent {
    activeModal = inject(NgbActiveModal);
    @Input() characterization: string;
}
