import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { AccountService, AlertService } from '@app/_services';
import { MustMatch } from '@app/_helpers';
import { UpdateSecretsComponent } from '@app/_components/update-secrets.component';

@Component({ templateUrl: 'update.component.html' })
export class UpdateComponent implements OnInit {
    account = this.accountService.accountValue!;
    form!: FormGroup;
    submitting = false;
    submitted = false;
    deleting = false;

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private accountService: AccountService,
        private alertService: AlertService,
        private modalService: NgbModal
    ) { }

    ngOnInit() {
        this.form = this.formBuilder.group({
            firstName: [this.account.firstName, Validators.required],
            lastName: [this.account.lastName, Validators.required],
            email: [this.account.email, [Validators.required, Validators.email]],
            password: ['', [Validators.minLength(6)]],
            confirmPassword: [''],
            apiKeys: [this.account.apiKeys],
        }, {
            validators: [MustMatch('password', 'confirmPassword')]
        });
        console.log("Form value:", this.form.value)
    }

    // convenience getter for easy access to form fields
    get f() { return this.form.controls; }

    updateSecrets() {
        let ref = this.modalService.open(UpdateSecretsComponent, { centered: true, size: 'lg' });
        ref.componentInstance.userPlatformMap = this.form.value.apiKeys;
        ref.result.then((resultado) => {
            this.form.patchValue({ apiKeys: resultado });
            this.accountService.patch(this.account.id!, { apiKeys: resultado })
            .pipe(first())
            .subscribe({
                next: () => {
                    this.alertService.success('API Keys & Secrets updated successfully');
                },
                error: error => {
                    this.alertService.error(error);
                }
            });
        }, () => { console.log("Edición cancelada") });
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
        this.accountService.update(this.account.id!, this.form.value)
            .pipe(first())
            .subscribe({
                next: () => {
                    this.alertService.success('Update successful', { keepAfterRouteChange: true });
                    this.router.navigate(['../'], { relativeTo: this.route });
                },
                error: error => {
                    this.alertService.error(error);
                    this.submitting = false;
                }
            });
    }

    onDelete() {
        if (confirm('Are you sure?')) {
            this.deleting = true;
            this.accountService.delete(this.account.id!)
                .pipe(first())
                .subscribe(() => {
                    this.alertService.success('Account deleted successfully', { keepAfterRouteChange: true });
                });
        }
    }
}