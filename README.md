Social List Sharing Platform (name in progress) 
Project Description: 
Making a social media web app built around lists, users are able to create and share ranked or unranked lists on the topic of their choice (favorite movies, video games, restaurants etc.). You can discover / connect with others by following other users, searching topics, liking and commenting on content.

Features planned:
Creating Lists
Social Feed
Follow System
Like & Comment
Private Lists
User Profiles
Search & Discovery (based around filters)


Sprint 1 - Project setup, environment (basic django app), agile planning
Sprint 2 - User authentication, list creation
Sprint 3 - Frontend styling updates, personal profile pages, clickable usernames
Sprint 4 - Feed & Profile Functionality

  Likes
  - Users can like any list from the feed or a profile page
  - Like count is displayed on each card
  - Like button highlights when active; clicking again unlikes

  Comments
  - Users can comment on any list directly from the feed or profile page
  - Comments are expandable per card using a collapsible section
  - Comment count displayed on each card; shows all existing comments with author links

  Profile Tabs
  - Profile pages now have three tabs: Posts, Liked, and Commented
  - Posts tab shows lists created by that user
  - Liked tab shows all lists the user has liked (with author info)
  - Commented tab shows all lists the user has commented on (with author info)
  - Profile stats show Lists, Followers, Following, and Liked counts

  Follow System
  - Users can follow and unfollow each other from any profile page
  - Button shows Follow, Unfollow, or Follow Back depending on relationship
  - "Follows you" badge shown when viewing a profile of someone who follows you
  - Followers and Following counts are clickable, leading to a dedicated user list page
  - Each user list page shows avatars, usernames, and follow/unfollow buttons

  Feed Tabs
  - Feed is split into two tabs: Following and Explore
  - Following tab shows only posts from users you follow plus your own
  - Explore tab shows posts from users you do not follow
  - Empty states guide users to explore or start following

  Avatar Colors
  - Users can pick a color for their letter avatar from a palette of 10 preset colors
  - Color applies everywhere: feed cards, profile pages, compose bar, follower/following lists
  - Accessible via the Settings page linked in the nav bar
  - Color previews live in the settings UI before saving
