'use client';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import * as z from 'zod';

const profileSchema = z.object({
  username: z
    .string()
    .min(3, {
      message: 'Username must be at least 3 characters.',
    })
    .max(28, {
      message: 'Username cannot be longer than 28 characters.',
    }),
  name: z.optional(
    z.string().max(75, {
      message: 'Username cannot be longer than 75 characters.',
    })
  ),
});

export default function ProfileForm() {
  const form = useForm<z.infer<typeof profileSchema>>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      username: '',
      name: '',
    },
  });

  async function updateProfile(values: z.infer<typeof profileSchema>) {}

  async function onSubmit(values: z.infer<typeof profileSchema>) {
    try {
      await updateProfile(values);
      form.reset({ username: values.username, name: values.name });
    } catch (err) {}
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className='flex w-full items-start gap-4'
      >
        <div className='flex w-96 flex-col gap-4'>
          <FormField
            control={form.control}
            name='name'
            render={({ field }) => (
              <FormItem>
                <FormLabel>Full name</FormLabel>
                <FormControl>
                  <Input placeholder='first last' {...field} />
                </FormControl>
                <FormDescription>This is your full name.</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <Button
            type='submit'
            className='w-full'
            disabled={!form.formState.isDirty || form.formState.isSubmitting}
          >
            Update profile
          </Button>
        </div>
      </form>
    </Form>
  );
}
