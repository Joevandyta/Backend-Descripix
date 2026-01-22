# Backend-Descripix
# Desripix API Documentation

## Overview

The Desripix API is a comprehensive image caption management system that allows users to generate, save, edit, and manage captions for images. The API provides OAuth-based authentication and JWT token management for secure access to caption-related operations.

## Base URL

The API uses a configurable base URL stored in the `{{baseURL}}` variable. Set this variable in your environment to match your deployment:

```
{{baseURL}}
```

## Authentication

This API uses **Bearer Token Authentication** with JWT (JSON Web Tokens). All authenticated requests require a valid access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Authentication Flow

1. **OAuth Login** - Authenticate using OAuth provider (Google)
2. **Token Refresh** - Refresh expired access tokens using refresh token
3. **Token Verify** - Validate token status and expiration
4. **Logout** - Invalidate current session

### Token Management

- **Access tokens** expire after a set period and must be refreshed
- **Refresh tokens** are used to obtain new access tokens without re-authentication
- Store tokens securely and never expose them in client-side code

## Main Features

### 🔐 Authentication & User Management
- OAuth-based login (Google)
- JWT token generation and refresh
- Token verification
- User profile management (view and edit)
- Secure logout

### 📝 Caption Management
- **Generate Captions** - AI-powered caption generation for images
- **Save Captions** - Store generated captions with metadata (author, location, device, date)
- **List Captions** - Retrieve all saved captions
- **View Caption Details** - Get detailed information about a specific caption
- **Edit Captions** - Update existing caption information
- **Delete Captions** - Remove captions from the system

## Getting Started

1. **Set up your environment**: Configure the `{{baseURL}}` variable with your API endpoint
2. **Authenticate**: Use the OAuth Login endpoint to obtain access tokens
3. **Set Bearer Token**: Add the access token to the collection's authorization settings
4. **Start making requests**: Use the caption management endpoints to work with your images

## Rate Limits

Please refer to your API service agreement for rate limiting information.

## Support

For API support, issues, or feature requests, please contact the development team.

## API Version

Current Version: 1.0
