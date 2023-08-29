import { NextRequest, NextResponse } from 'next/server'
import { revalidateTag } from 'next/cache'
 import { listWebsites } from '@/app/_db/mongo'

export async function GET(request: NextRequest) {
 
  return NextResponse.json({ revalidated: true, now: Date.now() })
}

export async function POST(request: NextRequest) {
   
  return NextResponse.json({ revalidated: true, now: Date.now() })
}