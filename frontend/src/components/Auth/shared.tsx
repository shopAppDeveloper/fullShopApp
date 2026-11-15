"use client";

import React, { useEffect, useState } from "react";

export const inputClass =
  "w-full rounded-lg border border-gray-3 bg-gray-1 px-5 py-3 outline-none focus:ring-2 focus:ring-blue/20";
export const buttonClass =
  "flex w-full items-center justify-center rounded-full bg-dark px-6 py-3 font-medium text-white duration-200 ease-out hover:bg-blue disabled:opacity-60";

export function Field({
  id,
  label,
  children,
}: {
  id: string;
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="mb-5">
      <label htmlFor={id} className="mb-2.5 block">
        {label}
      </label>
      {children}
    </div>
  );
}

export function ErrorBox({ message }: { message: string | null }) {
  if (!message) return null;
  return <p className="mb-5 rounded-md bg-red-light-6 px-4 py-3 text-sm text-red">{message}</p>;
}

export function InfoBox({ message }: { message: string | null }) {
  if (!message) return null;
  return <p className="mb-5 rounded-md bg-gray-1 px-4 py-3 text-sm text-dark">{message}</p>;
}

/** Counts down `seconds` after `start()`; used for the "resend code" button. */
export function useCountdown(seconds: number) {
  const [left, setLeft] = useState(0);
  useEffect(() => {
    if (left <= 0) return;
    const t = setTimeout(() => setLeft((v) => v - 1), 1000);
    return () => clearTimeout(t);
  }, [left]);
  return { left, start: () => setLeft(seconds) };
}

export function errorText(err: unknown, fallback: string) {
  return err instanceof Error ? err.message : fallback;
}
