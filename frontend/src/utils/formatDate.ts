export function formatDate(dateString: string): string {
  const date = new Date(dateString);

  return date.toLocaleDateString("en-us", {
    month: "2-digit",
    day: "2-digit",
    year: "numeric",
  });
}
