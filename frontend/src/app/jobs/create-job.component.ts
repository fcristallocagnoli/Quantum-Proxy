import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Provider, System } from '@app/_models';
import { ProviderService, SystemService } from '@app/_services';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
    templateUrl: './create-job.component.html',
})
export class CreateJobComponent {
    form!: FormGroup;
    submitting = false;
    submitted = false;
    deleting = false;

    selectedProvider: string;
    providers?: Provider[];
    systems?: System[];

    circuitInput?: string = '{"a":"hello","b":123}';

    constructor(
        public modal: NgbActiveModal,
        private providerService: ProviderService,
        private systemService: SystemService,
        private formBuilder: FormBuilder,
    ) { }

    ngOnInit() {
        this.form = this.formBuilder.group({
            name: ['', Validators.required],
            provider: ['', Validators.required],
            target: ['', Validators.required],
            shots: ['', Validators.required],
            qubits: ['', Validators.required],
            circuit: ['', Validators.required],
        });
        this.providerService.getAll().subscribe(providers => {
            this.providers = this.transformFromPython(providers);
            console.log(this.providers);
        });
    }

    get f() { return this.form.controls; }

    getProviders() {
        this.providerService.getAll().subscribe(providers => {
            this.providers = providers;
        });
    }

    getFilteredSystems() {
        const providerPID = this.f["provider"].value
        this.providerService.getByPid(providerPID).subscribe(provider => {
            this.systemService.getAll().subscribe(systems => {
                this.systems = systems.filter(s => provider["backends_ids"].includes(s.id));
            });
        });
    }

    normalizeName(name: string): string {
        return name.replace(/ /g, '-').replace(/\b\w/g, l => l.toUpperCase())
    }

    normalizeNameToURL(system: System): string {
        let bname = system.backend_name;
        let providerFrom = system.provider.provider_from;

        bname = bname.toLowerCase().replace(/ /g, '-');
        if (providerFrom) {
            bname = `${bname}-${providerFrom.toLowerCase()}`;
        }
        return bname;
    }

    onSubmit() {
        if (this.form.invalid) {
            return;
        }
        this.f["circuit"].setValue(JSON.parse(this.f["circuit"].value));
        this.modal.close(this.form.value);
    }

    // TODO: Acabar con estos metodos, usar el mismo nombre y ya esta
    transformFromPython(providers: any[]): Provider[] {
        return providers.map(provider => {
            return {
                ...provider,
                fromThirdParty: provider.from_third_party,
                fetchMethod: (provider.backend_request) ? provider.backend_request.fetch_method : null,
                thirdParty: (provider.third_party) ? {
                    id: provider.third_party.third_party_id,
                    name: provider.third_party.third_party_name
                } : null,
                systems: provider.backends_ids
            };
        });
    }

}
