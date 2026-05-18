export type BackendErrorData =
  | string
  | Array<unknown>
  | Record<string, unknown>
  | null;

interface ErrorWithResponse {
  response?: {
    data?: BackendErrorData;
  };
}

function isErrorWithResponse(error: unknown): error is ErrorWithResponse {
  return (
    typeof error === "object" &&
    error !== null &&
    "response" in error &&
    typeof (error as { response: unknown }).response === "object" &&
    (error as { response: unknown }).response !== null
  );
}

export function getBackendErrorData(
  error: unknown,
): BackendErrorData | undefined {
  if (!isErrorWithResponse(error)) {
    return undefined;
  }

  return (error as ErrorWithResponse).response?.data;
}

export function getBackendErrorMessage(error: unknown): string | undefined {
  const data = getBackendErrorData(error);

  if (typeof data === "string") {
    return data;
  }

  if (Array.isArray(data)) {
    return data.flatMap((value) => String(value)).join(" ");
  }

  if (data && typeof data === "object") {
    return Object.values(data)
      .flatMap((value) =>
        Array.isArray(value)
          ? value.map((item) => String(item))
          : String(value),
      )
      .join(" ");
  }

  return undefined;
}
