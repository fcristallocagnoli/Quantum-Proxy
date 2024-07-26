import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { WizardRoutingModule } from './wizard-routing.module';
import { WizardComponent } from './wizard.component';
import { StatusComponent, QueueComponent } from "../_components/properties.component";
import { NgbPaginationModule, NgbTooltip } from '@ng-bootstrap/ng-bootstrap';

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        WizardRoutingModule,
        StatusComponent,
        QueueComponent,
        NgbPaginationModule,
        NgbTooltip
    ],
    declarations: [
        WizardComponent
    ]
})
export class WizardModule { }