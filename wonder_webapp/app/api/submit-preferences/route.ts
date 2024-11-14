import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const res = await fetch("http://localhost:8000/submit-preferences", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    return NextResponse.json(data);
  } catch (e) {
    return NextResponse.json(
      { e: "Failed to process request" },
      { status: 500 },
    );
  }
}