import { TitleCasePipe } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
    selector: 'status',
    standalone: true,
    imports: [TitleCasePipe],
    template: `
        @switch (true) {
        @case (["running", "online", "available"].includes(status ?? 'N/A')) {
        <span class="text-success">
            <i class="fa-regular fa-circle-check"></i>
            {{ status | titlecase }} <br>
        </span>
        }
        @case (status === "offline") {
        <span class="text-danger">
            <i class="fa-regular fa-circle-xmark"></i>
            {{ status | titlecase }} <br>
        </span>
        }
        @case (status === "calibrating") {
        <span class="text-secondary">
            <i class="fa-regular fa-clock"></i>
            {{ status | titlecase }} <br>
        </span>
        }
        @case (!status) {
        <span class="text-warning">
            <i class="fa-regular fa-circle-question"></i>
            Unknown <br>
        </span>
        }
        @default {
        <span class="text-info">
            <span class="fa-stack" style="font-size: 8px;">
                <i class="fa-regular fa-circle fa-stack-2x"></i>
                <i class="fa-solid fa-info fa-stack-1x text-info fa-inverse"></i>
            </span>
            {{ status | titlecase }} <br>
        </span>
        }
        }
    `
})
export class StatusComponent {
    @Input() status?: string;

    constructor() { }

}


@Component({
    selector: 'queue',
    standalone: true,
    template: `
        @switch (queue?.type) {
        @case ("jobs_remaining") {
        Queued jobs:
        }
        @case ("avg_time") {
        Queue time:
        }
        @default {
        Queue:
        }
        }
    `
})
export class QueueComponent {
    @Input() queue?: { type: string, value: string };

    constructor() { }

}