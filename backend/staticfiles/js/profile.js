import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Profile() {
  const [profile, setProfile] = useState({
    name: "",
    username: "",
    email: "",
    university: "",
    skills: "",
    bio: "",
    avatar: ""
  });
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [avatarFile, setAvatarFile] = useState(null);

  useEffect(() => {
    axios.get("/api/profile/")
      .then(res => {
        setProfile(res.data); // Should match backend serializer fields
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleAvatarChange = (e) => {
    setAvatarFile(e.target.files[0]);
  };

  const saveProfile = async () => {
    const formData = new FormData();
    Object.keys(profile).forEach(key => {
      if (key !== "avatar") formData.append(key, profile[key]);
    });
    if (avatarFile) formData.append("avatar", avatarFile);

    try {
      await axios.put("/api/profile/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setEditMode(false);
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) return <p className="text-center mt-10">Loading profile...</p>;

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-2xl shadow-lg mt-10">
      <div className="flex flex-col items-center">
        <img
          src={avatarFile ? URL.createObjectURL(avatarFile) : profile.avatar}
          alt="Profile"
          className="w-32 h-32 rounded-full object-cover mb-4"
        />
        {editMode && (
          <input
            type="file"
            accept="image/*"
            onChange={handleAvatarChange}
            className="mb-4"
          />
        )}
        <h2 className="text-2xl font-bold mb-1">{profile.name}</h2>
        <p className="text-gray-600">@{profile.username}</p>
        <p className="text-gray-600">{profile.email}</p>
      </div>

      <div className="mt-6 space-y-4">
        <div>
          <label className="block font-semibold mb-1">University / Organization</label>
          {editMode ? (
            <input
              name="university"
              value={profile.university}
              onChange={handleChange}
              className="border p-2 rounded w-full"
            />
          ) : (
            <p>{profile.university}</p>
          )}
        </div>

        <div>
          <label className="block font-semibold mb-1">Skills</label>
          {editMode ? (
            <input
              name="skills"
              value={profile.skills}
              onChange={handleChange}
              className="border p-2 rounded w-full"
            />
          ) : (
            <p>{profile.skills}</p>
          )}
        </div>

        <div>
          <label className="block font-semibold mb-1">Bio</label>
          {editMode ? (
            <textarea
              name="bio"
              value={profile.bio}
              onChange={handleChange}
              className="border p-2 rounded w-full"
            />
          ) : (
            <p>{profile.bio}</p>
          )}
        </div>
      </div>

      <div className="flex justify-end mt-6">
        {editMode ? (
          <button
            onClick={saveProfile}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
          >
            Save
          </button>
        ) : (
          <button
            onClick={() => setEditMode(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Edit Profile
          </button>
        )}
      </div>
    </div>
  );
}
