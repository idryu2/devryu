import { useMemo, useState } from 'react'
import PostList from './PostList.jsx'
import WriteModal from './WriteModal.jsx'
import './blog.css'

export default function BlogSection({ posts, onAddPost }) {
  const [keyword, setKeyword] = useState('')
  const [isWriteOpen, setWriteOpen] = useState(false)

  // 검색: 제목/요약/카테고리에서 키워드 필터링
  const filtered = useMemo(() => {
    const q = keyword.trim().toLowerCase()
    if (!q) return posts
    return posts.filter((p) =>
      [p.title, p.excerpt, p.category]
        .join(' ')
        .toLowerCase()
        .includes(q),
    )
  }, [posts, keyword])

  return (
    <section className="blog" id="blog" aria-label="블로그">
      <div className="blog__head">
        <h2 className="blog__title">
          <span className="blog__title-mark">blog</span> 내 블로그
        </h2>
        <button
          className="blog__write-btn"
          type="button"
          onClick={() => setWriteOpen(true)}
        >
          ✏️ 글쓰기
        </button>
      </div>

      {/* 블로그 영역 전용 검색 */}
      <div className="blog__search">
        <input
          className="blog__search-input"
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="내 블로그 글 검색"
          aria-label="블로그 글 검색"
        />
        {keyword && (
          <button
            className="blog__search-clear"
            type="button"
            onClick={() => setKeyword('')}
            aria-label="검색어 지우기"
          >
            ✕
          </button>
        )}
      </div>

      <PostList posts={filtered} keyword={keyword} />

      {isWriteOpen && (
        <WriteModal
          onClose={() => setWriteOpen(false)}
          onSubmit={(post) => {
            onAddPost(post)
            setWriteOpen(false)
          }}
        />
      )}
    </section>
  )
}
