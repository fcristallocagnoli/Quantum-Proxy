import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { QueueComponent, StatusComponent, SystemPropsComponent } from '@app/_components/properties.component';
import { ComparativeRoutingModule } from './comparative-routing.module';
import { ComparativeComponent } from './comparative.component';
import { CompareProvidersComponent } from './compare-providers.component';
import { CompareSystemsComponent } from './compare-systems.component';

@NgModule({
    imports: [
        CommonModule,
        StatusComponent,
        QueueComponent,
        SystemPropsComponent,
        ReactiveFormsModule,
        ComparativeRoutingModule,
        FormsModule
    ],
    declarations: [
        ComparativeComponent,
        CompareProvidersComponent,
        CompareSystemsComponent
    ]
})
export class ComparativeModule { }