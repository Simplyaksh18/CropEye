// src/services/apiClient.ts

/**
 * Generic API client for making HTTP requests
 * Handles errors and provides consistent response format
 */

export class APIError extends Error {
  public status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
    this.name = "APIError";
  }
}

interface RequestOptions extends RequestInit {
  timeout?: number;
}

export const apiClient = async <T>(
  url: string,
  options: RequestOptions = {}
): Promise<T> => {
  const { timeout = 10000, ...fetchOptions } = options;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...fetchOptions,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...fetchOptions.headers,
      },
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new APIError(
        response.status,
        `HTTP Error ${response.status}: ${response.statusText}`
      );
    }

    const data = await response.json();
    return data as T;
  } catch (error) {
    clearTimeout(timeoutId);

    if (error instanceof APIError) {
      throw error;
    }

    if (error instanceof Error) {
      if (error.name === "AbortError") {
        throw new APIError(408, "Request timeout");
      }
      throw new APIError(0, error.message);
    }

    throw new APIError(0, "Unknown error occurred");
  }
};

export default apiClient;
