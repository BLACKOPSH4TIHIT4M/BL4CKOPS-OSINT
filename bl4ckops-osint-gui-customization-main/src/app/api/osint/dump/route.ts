import { NextRequest, NextResponse } from 'next/server';
import { googleSearch, delay } from '@/lib/google-search';

export async function POST(request: NextRequest) {
  try {
    const { moduleId } = await request.json();

    let query = '';
    let moduleName = '';

    // Module queries based on Python code
    switch (moduleId) {
      case 'A135': // DUMP EMAIL PASS
        query = 'filetype:xls username password email';
        moduleName = 'DUMP EMAIL PASS';
        break;
      case 'A166': // DUMP APACHE PASS
        query = "intext:'Index of /' +password.txt";
        moduleName = 'DUMP APACHE PASS';
        break;
      case 'A196': // DUMP SQL USER PASS
        query = 'filetype:sql user password';
        moduleName = 'DUMP SQL USER PASS';
        break;
      case 'A121': // DUMP APIKEYS
        query = "intitle:'index of' intext:apikey.txt";
        moduleName = 'DUMP APIKEYS';
        break;
      case 'A115': // DUMP COOKIES
        query = "intitle:'index of' intext:'cookies.txt'";
        moduleName = 'DUMP COOKIES';
        break;
      default:
        return NextResponse.json(
          { error: 'Invalid module ID' },
          { status: 400 }
        );
    }

    await delay(1000); // Simulate loading
    const results = await googleSearch(query, 10);

    return NextResponse.json({
      success: true,
      module: moduleName,
      moduleId,
      query,
      results,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('OSINT Dump error:', error);
    return NextResponse.json(
      { error: 'Failed to execute OSINT dump operation' },
      { status: 500 }
    );
  }
}
