import { CommonModule, JsonPipe, TitleCasePipe } from '@angular/common';
import { Component, Input, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { System } from '@app/_models';
import { NgbActiveModal, NgbModal, NgbTooltipModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
    selector: 'status',
    standalone: true,
    imports: [TitleCasePipe],
    template: `
        @switch (true) {
        @case (["running", "online", "available", "completed", "ready"].includes(status ?? 'N/A')) {
        <span style="color: #198754;">
            @if (icon) {
                <i class="fa-regular fa-circle-check"></i>
            }
            {{ status | titlecase }} <br>
        </span>
        }
        @case (status === "offline") {
        <span style="color: #dc3545;">
            @if (icon) {
                <i class="fa-regular fa-circle-xmark"></i>
            }
            {{ status | titlecase }} <br>
        </span>
        }
        @case (status === "calibrating") {
        <span style="color: #6c757d;">
            @if (icon) {
                <i class="fa-regular fa-clock"></i>
            }
            {{ status | titlecase }} <br>
        </span>
        }
        @case (!status) {
        <span style="color: #ffc107;">
            @if (icon) {
                <i class="fa-regular fa-circle-question"></i>
            }
            Unknown <br>
        </span>
        }
        @default {
        <span style="color: #0dcaf0;">
            @if (icon) {
                <span class="fa-stack" style="font-size: 8px;">
                    <i class="fa-regular fa-circle fa-stack-2x"></i>
                    <i class="fa-solid fa-info fa-stack-1x text-info fa-inverse"></i>
                </span>
            }
            {{ status | titlecase }} <br>
        </span>
        }
        }
    `
})
export class StatusComponent {
    @Input() status?: string;
    @Input() icon?: boolean = true;

    constructor() { }

}


@Component({
    selector: 'queue',
    standalone: true,
    template: `
        @switch (queue?.type) {
        @case ("jobs_remaining") {
        @if(!isTable) {
            Queued Jobs:
        }@else {
            Queued Jobs
        }
        }
        @case ("avg_time") {
        @if(!isTable) {
            Queue Time:
        }@else {
            Queue Time
        }
        }
        @default {
        @if(!isTable) {
            Queue:
        }@else {
            Queue
        }
        }
        }
    `
})
export class QueueComponent {
    @Input() queue?: { type: string, value: string };
    @Input() isTable?: boolean = false;

    constructor() { }

}

@Component({
    selector: 'system-props',
    standalone: true,
    imports: [CommonModule, StatusComponent, QueueComponent, RouterLink],
    template: `
        <div class="card">
            <table class="table table-striped table-borderless mb-0">
                <thead>
                    <tr>
                        <th style="width:20%;"></th>
                        @for (system of systems; track $index) {
                        <th style="width:30%;">
                            <!-- Se podria añadir el logo, haria falta obtener pagina web del proveedor -->
                            <!-- <img src="{{system.provider.website}}/favicon.ico" alt="Provider Logo" class="provider-logo"> -->
                            <a routerLink="/systems/{{ system.bid }}" class="link-underline link-underline-opacity-0"
                            style="color: inherit;">
                                {{ normalizeName(system.backend_name) }}
                                {{ (system.provider.provider_from ? ' (' + system.provider.provider_from + ')' : '') }}
                            </a>
                        </th>
                    }
                    </tr>
                </thead>
                <tbody>
                    <!-- extra fields (in common) -->
                    <tr>
                        <td>Provider</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.provider.provider_name }}
                            {{ system.provider.provider_from ? '(' + system.provider.provider_from + ')' : ''}}
                        </td>
                        }
                    </tr>
                    <tr>
                        <td>Status</td>
                        @for (system of systems; track $index) {
                        <td>
                            <status [status]="system.status"></status>
                        </td>
                        }
                    </tr>
                    <tr>
                        <td>Qubits</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.qubits}}
                        </td>
                        }
                    </tr>
                    <tr>
                        <td>Queue</td>
                        @for (system of systems; track $index) {
                        <td>
                            <queue [queue]="system.queue"></queue>
                            {{ system.queue?.value ?? 'N/A' }}
                        </td>
                        }
                    </tr>
                    <!-- extra fields (ionq) -->
                    @if (anyIsDefined(systems, 'degraded')) {
                    <tr>
                        <td>Degraded</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.degraded ?? 'N/A' }}
                        </td>
                        }
                    </tr>
                    }
                    @if (anyIsDefined(systems, 'has_access')) {
                    <tr>
                        <td>Has Access</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.has_access ?? 'N/A' }}
                        </td>
                        }
                    </tr>
                    }
                    @if (anyIsDefined(systems, 'characterization')) {
                    <tr>
                        <td>Characterization</td>
                        @for (system of systems; track $index) {
                        @if (system.characterization) {
                        <td>
                            <button class="btn btn-primary btn-sm" (click)="openModal(system)">View
                                Characterization</button>
                        </td>
                        }@else {
                        <td>N/A</td>
                        }
                        }
                    </tr>
                    }
                    <!-- extra fields (braket) -->
                    @if (anyIsDefined(systems, 'gates_supported')) {
                    <tr>
                        <td>Gates Supported</td>
                        @for (system of systems; track $index) {
                        @if (system.gates_supported) {
                        <td>{{ system.gates_supported.join(', ') }}</td>
                        }@else {
                        <td>N/A</td>
                        }
                        }
                    </tr>
                    }
                    @if (anyIsDefined(systems, 'shots_range')) {
                    <tr>
                        <td>Shots Range</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.shots_range?.min ?? 'N/A' }} - {{ system.shots_range?.max ?? 'N/A' }}
                        </td>
                        }
                    </tr>
                    }
                    @if (anyIsDefined(systems, 'device_cost')) {
                    <tr>
                        <td>Device Cost</td>
                        @for (system of systems; track $index) {
                        @if (system.device_cost) {
                        <td>{{ system.device_cost.price | currency }}/{{ system.device_cost.unit }}</td>
                        }@else {
                        <td>N/A</td>
                        }
                        }
                    </tr>
                    }
                    <!-- extra fields (rigetti) -->
                    @if (anyIsDefined(systems, 'rep_rate')) {
                    <tr>
                        <td>Rep Rate</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.rep_rate ?? 'N/A' }}
                        </td>
                        }
                    </tr>
                    }
                    @if (anyIsDefined(systems, 'median_t1')) {
                    <tr>
                        <td>Median T1</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.median_t1 ?? 'N/A' }}
                        </td>
                        }
                    </tr>
                    }
                    @if (anyIsDefined(systems, 'median_t2')) {
                    <tr>
                        <td>Median T2</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.median_t2 ?? 'N/A' }}
                        </td>
                        }
                    </tr>
                    }
                    <!-- extra fields (ibm) -->
                    @if (anyIsDefined(systems, 'basis_gates')) {
                    <tr>
                        <td>Basis Gates</td>
                        @for (system of systems; track $index) {
                        @if (system.basis_gates) {
                        <td>{{ system.basis_gates.join(', ') }}</td>
                        }@else {
                        <td>N/A</td>
                        }
                        }
                    </tr>
                    }
                    @if (anyIsDefined(systems, 'clops_h')) {
                    <tr>
                        <td>Clops H</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.clops_h ?? 'N/A' }}
                        </td>
                        }
                    </tr>
                    }
                    @if (anyIsDefined(systems, 'credits_required')) {
                    <tr>
                        <td>Credits Required</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.credits_required ?? 'N/A' }}
                        </td>
                        }
                    </tr>
                    }
                    @if (anyIsDefined(systems, 'max_experiments')) {
                    <tr>
                        <td>Max Experiments</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.max_experiments ?? 'N/A' }}
                        </td>
                        }
                    </tr>
                    }
                    @if (anyIsDefined(systems, 'max_shots')) {
                    <tr>
                        <td>Max Shots</td>
                        @for (system of systems; track $index) {
                        <td>
                            {{ system.max_shots ?? 'N/A' }}
                        </td>
                        }
                    </tr>
                    }
                    <tr>
                        <td>Last Checked</td>
                        @for (system of systems; track $index) {
                        <td>{{ system.last_checked | date: 'dd/MM/yy, HH:mm' }}</td>
                        }
                    </tr>
                </tbody>
            </table>
        </div>
    `,
    styles: [`
        .provider-logo {
            width: 30px;
            height: auto;
            margin-right: 10px;
        }
    `]
})
export class SystemPropsComponent {
    @Input() systems: System[];

    constructor(private modalService: NgbModal) { }

    openModal(system: System) {
        const modalRef = this.modalService.open(NgbdModalContent);
        modalRef.componentInstance.characterization = system.characterization;
    }

    anyIsDefined(systems: System[], field: string): boolean {
        return systems.some(sys => sys[field] !== undefined);
    }

    normalizeName(name: string): string {
        return name.replace(/ /g, '-').replace(/\b\w/g, l => l.toUpperCase())
    }

}


@Component({
    selector: 'ngbd-modal-content',
    standalone: true,
    template: `
    <div class="modal-header">
        <h4 class="modal-title">
            Characterization
            <a style="cursor: pointer;" (click)="openModal()">
                <i class="fa-regular fa-circle-question" style="font-size: 16px;"
                placement="bottom" ngbTooltip="Click for info about characterization"></i>
            </a>
        </h4>
        <button type="button" class="btn-close" aria-label="Close" (click)="activeModal.dismiss('Cross click')"></button>
    </div>
    <div class="modal-body">
        <pre>{{ characterization | json }}</pre>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary" (click)="activeModal.close('Close click')">Close</button>
    </div>
    `,
    imports: [JsonPipe, NgbTooltipModule]
})
export class NgbdModalContent {
    activeModal = inject(NgbActiveModal);
    @Input() characterization: string;

    constructor(private modalService: NgbModal) { }

    openModal() {
        this.modalService.open(NgbdModalExplaination, { centered: true });
    }
}

@Component({
    selector: 'ngbd-modal-explaination',
    standalone: true,
    template: `
    <div class="modal-header">
        <h4 class="modal-title">
            Characterization explaination
        </h4>
        <button type="button" class="btn-close" aria-label="Close" (click)="activeModal.dismiss('Cross click')"></button>
    </div>
    <div class="modal-body">
        <p><strong>date:</strong> Time of the measurement, from Unix epoch in seconds.</p>
        <p><strong>qubits:</strong> The number of qubits available.</p>
        <p><strong>fidelity:</strong> Fidelity for single-qubit ('1q') and two-qubit ('2q') gates, and State Preparation and Measurement ('spam') operations. Currently provides only mean fidelity; additional statistical data will be added in the future.</p>
        <p><strong>timing:</strong> Time, in seconds, of various system properties: 't1' time, 't2' time, '1q' gate time, '2q' gate time, 'readout' time, and qubit 'reset' time.</p>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary" (click)="activeModal.close('Close click')">Close</button>
    </div>
    `,
    imports: []
})
export class NgbdModalExplaination {
    activeModal = inject(NgbActiveModal);
}

