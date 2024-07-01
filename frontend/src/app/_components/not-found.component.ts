import { Component } from '@angular/core';

@Component({
    template: `
    <div class="p-4">
        <div class="container">
            <div class="error-code">404</div>
            <div class="error-message">Page Not Found</div>
            <p class="mb-4">Sorry, the page you are looking for does not exist.</p>
            <a href="/" class="btn btn-primary">Go to Homepage</a>
        </div>
    </div>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f8f9fa;
            color: #343a40;
        }

        .container {
            text-align: center;
        }

        .error-code {
            font-size: 6rem;
            font-weight: 700;
        }

        .error-message {
            font-size: 1.5rem;
            margin-bottom: 2rem;
        }
    </style>
    `
})
export class NotFoundComponent {
    constructor() { }
}