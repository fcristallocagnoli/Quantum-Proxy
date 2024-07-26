import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
    template: `
    <div class="p-4">
        <div class="container text-center">
            <div class="error-code" style="font-size: 6rem; font-weight: 700;">
                404
            </div>
            <div class="mb-4" style="font-size: 1.5rem;">
                Page Not Found
            </div>
            <p class="mb-4">
                Sorry, the page you are looking for does not exist.
            </p>
            <a routerLink="/" class="btn btn-primary">Go to Homepage</a>
        </div>
    </div>
    `,
    standalone: true,
    imports: [RouterLink]
})
export class NotFoundComponent {
    constructor() { }
}