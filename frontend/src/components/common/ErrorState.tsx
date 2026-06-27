export function ErrorState({ message = "Something went wrong." }: { message?: string }) {
  return (
    <div className="border-destructive/30 bg-destructive/10 text-destructive rounded-md border p-4 text-sm">
      {message}
    </div>
  );
}
