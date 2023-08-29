import { MongoClient, ObjectId } from 'mongodb';
import { Crawl } from '../_types/crawls';
import { Website } from '../_types/websites';

const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');
const db = client.db(process.env.MONGO_DBNAME || 'open-crawler');
const collections = {
    websites: db.collection('websites'),
    crawls: db.collection('crawls'),
}

export async function listWebsites() {
    return collections.websites.find<Website>({}).toArray();
}
export async function getWebsite(id: string) {
    const websites = await collections.websites.findOne<Website>({ _id: new ObjectId(id) });
    const crawls = await collections.crawls.findOne<Crawl>({ _id: new ObjectId(id) });
    return { ...websites, ...crawls };
}


export default db;