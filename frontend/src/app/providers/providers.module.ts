import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

import { ProvidersRoutingModule } from './providers-routing.module';
import { ProvidersComponent } from './providers.component';
import { ViewProviderComponent } from './view-provider.component';
import { QueueComponent, StatusComponent } from '@app/_components/properties.component';

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        ProvidersRoutingModule,
        StatusComponent,
        QueueComponent
    ],
    declarations: [
        ProvidersComponent,
        ViewProviderComponent
    ]
})
export class ProvidersModule { }