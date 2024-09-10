import { Component, OnInit } from '@angular/core';
import { AlertService, SystemService } from '@app/_services';
import { HelperService } from '@app/_services/helper.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ConfirmationModal } from '../../_components';

@Component({ templateUrl: 'database.component.html' })
export class DatabaseComponent implements OnInit {

    fetching: boolean = false;
    deleting: boolean = false;

    updatingDB: boolean = this.fetching || this.deleting;

    isDatabaseEmpty: boolean = false;

    constructor(
        private systemService: SystemService,
        private alertService: AlertService,
        private helperService: HelperService,
        private modalService: NgbModal
    ) { }

    ngOnInit(): void {
        this.alertService.clear();

        // check if every collection is empty
        const collections = ['providers', 'backends'];
        this.isDatabaseEmpty = collections.every((coll) => {
            this.helperService.countDocuments(coll).subscribe((data) => {
                return data.count === 0;
            });
        });
    }

    updateSystems() {
        let ref = this.modalService.open(ConfirmationModal);
        ref.componentInstance.title = "Update Confirmation";
        ref.componentInstance.bodyText = "Are you sure that you want to update all systems?";
        ref.result.then((result) => {
            if (result === 'ok click') {
                this.fetching = true;
                this.alertService.info(`
                    <h4>Updating systems</h4>
                    <p>Please wait for the task to be finished</p>
                `,);
                this.systemService.refreshData({})
                    .subscribe({
                        next: () => {
                            this.fetching = false;
                            this.alertService.success(`
                                <h4>Systems updated</h4>
                                <p>Reload where necessary to get the new updated data</p>
                            `, { autoClose: false });
                        },
                        error: error => {
                            this.alertService.error(`
                                <h4>Error updating systems</h4>
                                <p>${error}</p>
                            `);
                        }
                    });
            }
        });
    }

    // El boton de borrar esta desactivado hasta que se implemente el de inicializar
    deleteData() {
        let ref = this.modalService.open(ConfirmationModal);
        ref.componentInstance.title = "Delete Confirmation";
        ref.componentInstance.bodyText = "Are you sure that you want to delete all data?";
        ref.componentInstance.buildModal("deletion")
        ref.result.then((result) => {
            if (result === 'ok click') {
                this.deleting = true;
                this.alertService.info(`
                    <h4>Deleting systems</h4>
                    <p>Please wait for the task to be finished</p>
                `);
                this.helperService.deleteAllData()
                    .subscribe({
                        next: () => {
                            this.deleting = false;
                            this.isDatabaseEmpty = true;
                            this.alertService.success(`
                                <h4>Data deleted successfully</h4>
                                <p>Refetch to get new data</p>
                            `);
                        },
                        error: error => {
                            this.alertService.error(`
                                <h4>Error deleting data</h4>
                                <p>${error}</p>
                            `);
                        }
                    });
            }
        });
    }

    // [ ]: Configurar la inicialización en el backend
    initData() {
    }

}