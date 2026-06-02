import { useState } from 'react'

const CATEGORIES = ['일상', '여행', '개발', '요리', '리뷰']

export default function WriteModal({ onClose, onSubmit }) {
  const [title, setTitle] = useState('')
  const [excerpt, setExcerpt] = useState('')
  const [category, setCategory] = useState(CATEGORIES[0])
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!title.trim()) {
      setError('제목을 입력해 주세요.')
      return
    }
    onSubmit({
      title: title.trim(),
      excerpt: excerpt.trim() || '내용 미리보기가 없습니다.',
      category,
    })
  }

  return (
    <div
      className="modal-backdrop"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-label="블로그 글쓰기"
    >
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal__head">
          <h3 className="modal__title">글쓰기</h3>
          <button
            className="modal__close"
            type="button"
            onClick={onClose}
            aria-label="닫기"
          >
            ✕
          </button>
        </div>

        <form className="write-form" onSubmit={handleSubmit}>
          <label className="write-form__label">
            제목
            <input
              className="write-form__input"
              type="text"
              value={title}
              onChange={(e) => {
                setTitle(e.target.value)
                if (error) setError('')
              }}
              placeholder="제목을 입력하세요"
              autoFocus
            />
          </label>

          <label className="write-form__label">
            카테고리
            <select
              className="write-form__input"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              {CATEGORIES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </label>

          <label className="write-form__label">
            내용
            <textarea
              className="write-form__input write-form__textarea"
              value={excerpt}
              onChange={(e) => setExcerpt(e.target.value)}
              placeholder="내용을 입력하세요"
              rows={5}
            />
          </label>

          {error && <p className="write-form__error">{error}</p>}

          <div className="write-form__actions">
            <button
              className="btn btn--ghost"
              type="button"
              onClick={onClose}
            >
              취소
            </button>
            <button className="btn btn--primary" type="submit">
              발행
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
