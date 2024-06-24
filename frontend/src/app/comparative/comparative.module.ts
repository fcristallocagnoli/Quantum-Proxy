import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { QueueComponent, StatusComponent } from '@app/_components/properties.component';
import { ComparativeRoutingModule } from './comparative-routing.module';
import { ComparativeComponent } from './comparative.component';
import { CompareProvidersComponent } from './compare-providers.component';

@NgModule({
    imports: [
        CommonModule,
        StatusComponent,
        QueueComponent,
        ReactiveFormsModule,
        ComparativeRoutingModule,
        FormsModule
    ],
    declarations: [
        ComparativeComponent,
        CompareProvidersComponent
    ]
})
export class ComparativeModule { }