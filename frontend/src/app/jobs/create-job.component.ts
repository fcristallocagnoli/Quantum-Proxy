import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Provider, System } from '@app/_models';
import { AlertService, ProviderService, SystemService } from '@app/_services';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
    templateUrl: './create-job.component.html',
})
export class CreateJobComponent {
    form!: FormGroup;

    selectedProvider: string = 'native.ionq';
    selectedTarget: string = 'simulator';
    providers?: Provider[];
    systems?: System[];

    circuitInput?: string = '{"a":"hello","b":123}';

    constructor(
        public modal: NgbActiveModal,
        private providerService: ProviderService,
        private systemService: SystemService,
        private formBuilder: FormBuilder,
        private alertService: AlertService
    ) { }

    ngOnInit() {
        this.form = this.formBuilder.group({
            name: ['', Validators.required],
            provider: ['', Validators.required],
            target: ['', Validators.required],
            shots: ['', Validators.required],
            qubits: ['', Validators.required],
            circuit: ['', Validators.required],
            noiseModel: [''],
        });
        this.providerService.getAll().subscribe(providers => {
            this.providers = providers;
        });
        this.getFilteredSystems(this.selectedProvider);
    }

    get f() { return this.form.controls; }

    getProviders() {
        this.providerService.getAll().subscribe(providers => {
            this.providers = providers;
        });
    }

    getFilteredSystems(providerPID: string = this.f["provider"].value) {
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
            console.log(this.form);
            this.alertService.error("Form is invalid");
            return;
        }
        this.f["circuit"].setValue(JSON.parse(this.f["circuit"].value));
        this.modal.close(this.form.value);
    }

    fillWithExample(example: string) {
        switch (example) {
            case 'bell':
                this.f["name"].setValue("Bell State Example");
                this.f["provider"].setValue("native.ionq");
                this.getFilteredSystems();
                this.f["target"].setValue("simulator");
                this.f["shots"].setValue(1000);
                this.f["qubits"].setValue(2);
                this.f["circuit"].setValue('[{"gate": "h", "target": 0},{"gate": "cnot","target": 1,"control": 0}]');
                break;
            case 'ghz':
                this.f["name"].setValue("GHZ State Example");
                this.f["provider"].setValue("native.ionq");
                this.getFilteredSystems();
                this.f["target"].setValue("simulator");
                this.f["shots"].setValue(1000);
                this.f["qubits"].setValue(4);
                this.f["circuit"].setValue('[{"gate": "h","target": 0},{"gate": "cnot","control": 0,"target": 1},{"gate": "cnot","control": 0,"target": 2},{"gate": "cnot","control": 0,"target": 3}]');
                break;
            case 'toffoli':
                this.f["name"].setValue("Toffoli gate Example");
                this.f["provider"].setValue("native.ionq");
                this.getFilteredSystems();
                this.f["target"].setValue("simulator");
                this.f["shots"].setValue(1000);
                this.f["qubits"].setValue(3);
                this.f["circuit"].setValue('[{"gate": "cnot","target": 0,"controls": [1, 2]}]');
                break;
            case 'qft3':
                this.f["name"].setValue("Quantum Fourier Transform Example");
                this.f["provider"].setValue("native.ionq");
                this.getFilteredSystems();
                this.f["target"].setValue("simulator");
                this.f["shots"].setValue(1000);
                this.f["qubits"].setValue(3);
                this.f["circuit"].setValue('[{"gate": "h", "target": 2},{"gate": "s", "target": 1, "control": 2},{"gate": "t", "target": 0, "control": 2},{"gate": "h", "target": 1},{"gate": "s", "target": 0, "control": 1},{"gate": "h", "target": 0},{"gate": "swap", "targets": [0,2]}]');
                break;
            case 'clear':
                this.f["name"].setValue("");
                this.f["provider"].setValue("native.ionq");
                this.getFilteredSystems();
                this.f["target"].setValue("simulator");
                this.f["shots"].setValue("");
                this.f["qubits"].setValue("");
                this.f["circuit"].setValue('');
                break;
        }
    }

}
