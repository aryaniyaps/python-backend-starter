import AppearanceForm from '@/components/settings/appearance/appearance-form';

export default function AppearanceSettingsPage() {
  return (
    <div className='space-y-6'>
      <div>
        <h3 className='text-lg font-medium'>Appearance</h3>
        <p className='text-muted-foreground text-sm'>
          Manage how your app looks here.
        </p>
      </div>
      <AppearanceForm />
    </div>
  );
}
