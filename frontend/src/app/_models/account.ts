import { Role } from './role';

export class APIKeys {
    [platform: string]: { apiKeys: Map<string, string> };
}

export class Account {
    id?: string;
    firstName?: string;
    lastName?: string;
    email?: string;
    role?: Role;
    apiKeys?: APIKeys;
    jwtToken?: string;
    dateCreated?: Date;
}