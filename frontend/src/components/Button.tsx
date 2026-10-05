import type { ButtonHTMLAttributes } from "react";

type ButtonVariant =
  | "primary"
  | "secondary"
  | "danger";

type ButtonProps =
  ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: ButtonVariant;
  };

function Button({
  variant = "secondary",
  className = "",
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={`button ${variant}-button ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;