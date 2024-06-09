import { Component, OnInit } from '@angular/core';
import { AlertService, SystemService } from '@app/_services';

@Component({ templateUrl: 'database.component.html' })
export class DatabaseComponent implements OnInit {

    fetching: boolean = false;

    constructor(private systemService: SystemService, private alertService: AlertService) { }

    ngOnInit(): void {
        this.alertService.clear();
    }

    updateSystems() {
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
                    `);
                },
                error: error => {
                    console.log(error);
                }
            });
    }

}