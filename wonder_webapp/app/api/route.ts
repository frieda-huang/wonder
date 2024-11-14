import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const requestedData = await request.json();
    const res = await fetch("http://localhost:8000/preferences", {
      method: "POST",
      body: JSON.stringify(requestedData),
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
