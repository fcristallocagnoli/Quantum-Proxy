import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { WizardRoutingModule } from './wizard-routing.module';
import { WizardComponent } from './wizard.component';
import { StatusComponent, QueueComponent } from "../_components/properties.component";
import { NgbPaginationModule, NgbTooltip } from '@ng-bootstrap/ng-bootstrap';

import { CarouselModule } from 'primeng/carousel';

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        WizardRoutingModule,
        StatusComponent,
        QueueComponent,
        NgbPaginationModule,
        NgbTooltip,
        CarouselModule
    ],
    declarations: [
        WizardComponent
    ]
})
export class WizardModule { }