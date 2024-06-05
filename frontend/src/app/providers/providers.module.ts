import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

import { ProvidersRoutingModule } from './providers-routing.module';
import { ProvidersComponent } from './providers.component';
import { ViewProviderComponent } from './view-provider.component';

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        ProvidersRoutingModule
    ],
    declarations: [
        ProvidersComponent,
        ViewProviderComponent
    ]
})
export class ProvidersModule { }