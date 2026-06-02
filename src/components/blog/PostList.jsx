export default function PostList({ posts, keyword }) {
  if (posts.length === 0) {
    return (
      <p className="blog__empty">
        {keyword
          ? `'${keyword}'에 대한 글이 없어요.`
          : '아직 작성한 글이 없어요. 첫 글을 써보세요!'}
      </p>
    )
  }

  return (
    <ul className="post-list">
      {posts.map((post) => (
        <li key={post.id} className="post-item">
          <div className="post-item__top">
            <span className="post-item__category">{post.category}</span>
            <span className="post-item__date">{post.date}</span>
          </div>
          <h3 className="post-item__title">{post.title}</h3>
          <p className="post-item__excerpt">{post.excerpt}</p>
          <span className="post-item__views">조회 {post.views}</span>
        </li>
      ))}
    </ul>
  )
}
