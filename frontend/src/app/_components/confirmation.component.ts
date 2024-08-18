import { Component, inject } from "@angular/core";
import { NgbActiveModal } from "@ng-bootstrap/ng-bootstrap";

@Component({
    template: `
        <div class="modal-header">
            <h4 class="modal-title">{{ title }}</h4>
            <button class="btn-close" aria-label="Close" (click)="activeModal.dismiss('Cross click')"></button>
        </div>
        <div class="modal-body">
            <span>{{ bodyText }}</span>
        </div>
        <div class="modal-footer">
            <button class="btn btn-{{dismissBtn}}" ngbAutofocus (click)="activeModal.dismiss('cancel click')">No</button>
            <button class="btn btn-{{confirmBtn}}" (click)="activeModal.close('ok click')">Yes</button>
        </div>
      `,
      standalone: true
})
export class ConfirmationModal {
    activeModal = inject(NgbActiveModal);

    title: string = "Confirmation";
    bodyText: string = "Are you sure that you want to proceed?";

    dismissBtn: string = "outline-secondary";
    confirmBtn: string = "primary";

    buildModal(modalType: string) {
        switch (modalType) {
            case "confirmation":
                this.title = "Confirmation";
                this.dismissBtn = "outline-secondary";
                this.confirmBtn = "success";
                break;
            case "deletion":
                this.title = "Delete Confirmation";
                this.dismissBtn = "secondary";
                this.confirmBtn = "danger";
                break;
            default:
                this.dismissBtn = "outline-secondary";
                this.confirmBtn = "success";
                break;
        }
    }
}