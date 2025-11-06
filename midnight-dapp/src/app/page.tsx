// File: src/app/page.tsx
// Location: /mnt/c/projects/midnight-infrastructure/midnight-dapp/src/app/page.tsx

// File: src/app/page.tsx
import WalletRegistry from '../components/WalletRegistry';
import MidnightPanel from '../components/MidnightPanel';
import DonationRouter from '../components/DonationRouter';

export default function Home() {
  return (
    <main className="p-8 space-y-6">
      <h1 className="text-3xl font-bold">Midnight Dashboard</h1>
      <WalletRegistry />
      <MidnightPanel />
      <DonationRouter />
    </main>
  );
}

