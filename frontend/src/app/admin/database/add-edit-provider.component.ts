import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AlertService, ProviderService } from '@app/_services';

@Component({ templateUrl: 'add-edit-provider.component.html' })
export class AddEditProviderComponent implements OnInit {
    form!: FormGroup;
    pid?: string;
    title!: string;
    loading = false;
    submitting = false;
    submitted = false;

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private alertService: AlertService,
        private providerService: ProviderService,
    ) { }

    ngOnInit() {
        this.pid = this.route.snapshot.params['pid'];

        this.form = this.formBuilder.group({
            provider: [''],
        });

        this.title = 'Create Provider';
        if (this.pid) {
            // edit mode
            this.title = 'Edit Provider';
            this.loading = true;
            this.providerService.getByPid(this.pid)
                .pipe(first())
                .subscribe(x => {
                    this.form.patchValue({ provider: JSON.stringify(x, null, "\t") });
                    this.loading = false;
                });
        }
    }

    // convenience getter for easy access to form fields
    get f() { return this.form.controls; }

    handleTab(event: any) {
        event.preventDefault();
        var start = event.target.selectionStart;
        var end = event.target.selectionEnd;
        event.target.value = event.target.value.substring(0, start) + '\t' + event.target.value.substring(end);
        event.target.selectionStart = event.target.selectionEnd = start + 1;
    }

    onSubmit() {
        this.submitted = true;

        // reset alerts on submit
        this.alertService.clear();

        // stop here if form is invalid
        if (this.form.invalid) {
            return;
        }

        this.submitting = true;

        // create or update provider based on id param
        let saveProvider;
        let message: string;
        if (this.pid) {
            saveProvider = () => this.providerService.update(this.pid!, JSON.parse(this.f["provider"].value));
            message = 'Provider updated successfully';
        } else {
            saveProvider = () => this.providerService.create(JSON.parse(this.f["provider"].value));
            message = 'Provider created successfully';
        }

        saveProvider()
            .pipe(first())
            .subscribe({
                next: () => {
                    this.alertService.success(message, { keepAfterRouteChange: true });
                    this.router.navigateByUrl('/admin/database/providers');
                },
                error: error => {
                    this.alertService.error(error);
                    this.submitting = false;
                }
            });
    }
}