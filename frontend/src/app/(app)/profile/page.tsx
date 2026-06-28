"use client";

import { useState } from "react";
import { toast } from "sonner";

import { Loading } from "@/components/common/Loading";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { updateProfile } from "@/store/slices/authSlice";
import type { User } from "@/types";

export default function ProfilePage() {
  const user = useAppSelector((s) => s.auth.user);

  // While the session is still loading, show a spinner.
  if (!user) return <Loading label="Loading profile..." />;

  return <ProfileForm user={user} />;
}

// Separate component so its form state initializes from the loaded user.
function ProfileForm({ user }: { user: User }) {
  const dispatch = useAppDispatch();
  const [name, setName] = useState(user.name);
  const [saving, setSaving] = useState(false);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    try {
      await dispatch(updateProfile({ name })).unwrap();
      toast.success("Profile updated");
    } catch (error) {
      toast.error(typeof error === "string" ? error : "Could not update profile");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="mx-auto max-w-lg">
      <h1 className="mb-4 text-2xl font-bold">My Profile</h1>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            {user.name}
            <Badge variant="secondary">{user.role}</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSave} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              {/* Email can't be changed. */}
              <Input id="email" value={user.email} disabled />
            </div>
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input id="name" value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <Button type="submit" disabled={saving || name.trim() === ""}>
              {saving ? "Saving..." : "Save changes"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
