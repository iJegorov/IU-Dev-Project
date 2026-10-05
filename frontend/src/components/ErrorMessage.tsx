type ErrorMessageProps = {
  message: string;
};

function ErrorMessage({
  message,
}: ErrorMessageProps) {
  if (!message) {
    return null;
  }

  return (
    <div className="error-message">
      <strong>Error</strong>
      <span>{message}</span>
    </div>
  );
}

export default ErrorMessage;