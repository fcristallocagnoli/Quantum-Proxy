import { Component, OnInit } from '@angular/core';
import { first } from 'rxjs/operators';

import { AccountService } from '@app/_services';
import { ConfirmationModal } from '@app/_components/confirmation.component';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({ templateUrl: 'list.component.html' })
export class ListComponent implements OnInit {
    accounts?: any[];

    constructor(
        private accountService: AccountService,
        private modalService: NgbModal
    ) { }

    ngOnInit() {
        this.accountService.getAll()
            .pipe(first())
            .subscribe(accounts => this.accounts = accounts);
    }

    deleteAccount(id: string) {
        let ref = this.modalService.open(ConfirmationModal);
        ref.componentInstance.buildModal("deletion");
        ref.componentInstance.bodyText = "Are you sure that you want to delete this account?";
        ref.result.then((result) => {
            if (result === 'ok click') {
                const account = this.accounts!.find(x => x.id === id);
                account.isDeleting = true;
                this.accountService.delete(id)
                    .pipe(first())
                    .subscribe(() => {
                        this.accounts = this.accounts!.filter(x => x.id !== id)
                    });
            }
        });
    }
}