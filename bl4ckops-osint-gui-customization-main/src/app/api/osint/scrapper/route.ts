import { NextRequest, NextResponse } from 'next/server';
import { googleSearch, delay } from '@/lib/google-search';

export async function POST(request: NextRequest) {
  try {
    const { moduleId, target, countryCode } = await request.json();

    if (!target) {
      return NextResponse.json(
        { error: 'Target domain is required' },
        { status: 400 }
      );
    }

    let queries: { query: string; type: string }[] = [];
    let moduleName = '';

    switch (moduleId) {
      case 'A235': // FILES SCRAPPING
        moduleName = 'FILES SCRAPPING';
        const fileTypes = ['pdf', 'txt', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'htm', 'html', 'zip', 'tar', 'flv', 'mp4', 'jpg', 'png', 'mp3', 'gz', 'bz2'];
        queries = fileTypes.map(type => ({
          query: `site:${target}.com filetype:${type}`,
          type: type.toUpperCase()
        }));
        break;

      case 'A312': // NUMBERS SCRAPPING
        if (!countryCode) {
          return NextResponse.json(
            { error: 'Country code is required for number scrapping' },
            { status: 400 }
          );
        }
        moduleName = 'NUMBERS SCRAPPING';
        queries = [{
          query: `site:${target}.com intext:Whatsapp ${countryCode}`,
          type: 'Phone Numbers'
        }];
        break;

      case 'A221': // EMAILS SCRAPPING
        moduleName = 'EMAILS SCRAPPING';
        const emailProviders = ['gmail', 'hotmail.com', 'yandex.com', 'yahoo.com', 'gmx.com', 'zoho.com', 'aol.com', 'email.com'];
        queries = emailProviders.map(provider => ({
          query: `site:${target}.com intext:@${provider}`,
          type: provider
        }));
        break;

      case 'A186': // PAGES SCRAPPING
        moduleName = 'PAGES SCRAPPING';
        const pageTypes = ['blog', 'security', 'complaint', 'documents', 'punishment', 'database', 'state', 'hospital', 'school', 'airport', 'railway'];
        queries = pageTypes.map(type => ({
          query: `site:${target} intext:${type}`,
          type: type.charAt(0).toUpperCase() + type.slice(1)
        }));
        break;

      case 'A189': // OTHER SCRAPPING
        moduleName = 'OTHER SCRAPPING';
        queries = [
          { query: `related:${target}.com`, type: 'Related Pages' },
          { query: `link:${target}.com`, type: 'Links' },
          { query: `info:${target}.com`, type: 'Info Page' }
        ];
        break;

      case 'A102': // PASS SCRAPPING
        moduleName = 'PASS SCRAPPING';
        queries = [
          { query: `site:${target}.com filetype:password`, type: 'Password Files 1' },
          { query: `site:${target}.com filetype:passwords`, type: 'Password Files 2' },
          { query: `site:${target}.com inurl:/etc/passwd`, type: 'Passwd Files' },
          { query: `site:${target}.com filetype:log.txt`, type: 'Log Files' }
        ];
        break;

      default:
        return NextResponse.json(
          { error: 'Invalid module ID' },
          { status: 400 }
        );
    }

    const allResults: any[] = [];

    // Execute searches with delay between each
    for (const { query, type } of queries) {
      try {
        await delay(2000); // 2 second delay between searches
        const results = await googleSearch(query, 10);
        allResults.push({
          type,
          query,
          results,
          count: results.length
        });
      } catch (error) {
        console.error(`Error searching ${type}:`, error);
        allResults.push({
          type,
          query,
          results: [],
          count: 0,
          error: 'Search failed'
        });
      }
    }

    return NextResponse.json({
      success: true,
      module: moduleName,
      moduleId,
      target,
      countryCode,
      results: allResults,
      totalCategories: allResults.length,
      totalResults: allResults.reduce((sum, r) => sum + r.count, 0),
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('OSINT Scrapper error:', error);
    return NextResponse.json(
      { error: 'Failed to execute OSINT scrapper operation' },
      { status: 500 }
    );
  }
}
