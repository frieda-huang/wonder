import Image from "next/image";

export default function Home() {
  return (
    <div className="flex justify-center">
      <Image
        src="/images/youcanjustdothings.jpeg"
        width={1000}
        height={1000}
        alt="You can just do things"
        style={{ borderRadius: "15px" }}
      />
    </div>
  );
}
